#!/usr/bin/env python3

import requests
import json

url_postings = "https://qcpi.questcdn.com/cdn/posting/?group=1950787&provider=1950787"
url_get_posting = "https://qcpi.questcdn.com/cdn/util/get_posting/?current_project_id={}&next_project_id=&prev_project_id="

url_all_postings = "https://qcpi.questcdn.com/cdn/browse_posting/"


LIMIT = 5



def main():
    print("Started")
    tableResp = requests.get(url_all_postings, headers={"Referer": url_postings})
    print("Got Table", tableResp)
    # print("JSON", table.text)
    # soup = BeautifulSoup(page.text, "html.parser")
    if tableResp.status_code != 200:
        print("Error Fetching Table")
        return 1
        
    table = json.loads(tableResp.text)
    if "result" in table and table["result"] == "ok":
        print("Table OK")
    else:
        print("Error in Table")
        print("Table", table)
        return 2
    print("Parsed JSON")

    scraped_data = []

    for i, data in enumerate(table["data"]):
        render_posting = data["render_my_posting"]
        start_i = render_posting.find("value=")
        questId = render_posting[start_i+6:render_posting.find(" ", start_i+7)]
        print("QuestId", questId)

        print("REQ", url_get_posting.format(questId))
        posting = requests.get(url_get_posting.format(questId), headers={"Referer": url_postings})
        # print("Posting HTML", posting.text)
        lower_html = posting.text.lower()

        start_loc = lower_html.find("est. value")
        est_val_start = lower_html.find(";\">", start_loc) + 3
        est_val = lower_html[est_val_start: lower_html.find("</td>", est_val_start + 1)]

        start_loc = lower_html.find("description:")
        desc_start = lower_html.find(";\">", start_loc) + 3
        desc = posting.text[desc_start: lower_html.find("</td>", desc_start + 1)]

        start_loc = lower_html.find("closing date: ")
        closing_date = posting.text[start_loc+14: lower_html.find("</b>", start_loc)]

        print("Est Val", est_val)
        print("Desc", desc)
        print("Closing Date", closing_date)

        scraped_data.append({
            "quest_id": questId,
            "est_value_notes": est_val,
            "description": desc,
            "closing_date": closing_date})

        if i >= LIMIT-1:
            break

    print("Writing Scraped Data to File")
    with open("scraped_data.json", "w") as file:
        json.dump(scraped_data, file, indent=2)
    print("DONE")


if __name__ == "__main__":
    main()

