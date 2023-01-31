# encoding: utf-8
# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
from time import sleep
import time
import requests
from random import randint
from html.parser import HTMLParser
import json
import csv
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                           'like Gecko) Chrome/109.0.0.0 Safari/537.36'}


class SearchEngine:
    @staticmethod
    def search(query, sleep=True):
        if sleep:  # Prevents loading too many pages too soon
            time.sleep(randint(5, 10))
        temp_url = '%20'.join(query.split())  # for adding + between words for the query
        url = 'https://www.ask.com/web?q=' + temp_url
        html = requests.get(url, headers=USER_AGENT)
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, "html.parser")
        # print(soup.prettify(encoding='gbk').decode(encoding='gbk'))
        new_results = SearchEngine.scrape_search_result(soup)
        askResultDict[query] = new_results
        return new_results

    @staticmethod
    def scrape_search_result(soup):
        raw_results = soup.find_all("a", {"class": "PartialSearchResults-item-title-link result-link"})
        results = []
        cnt = 1
        # implement a check to get only 10 results and also check that URLs must not be duplicated
        for result in raw_results:
            link = result.get('href')
            print("\t{}:{}".format(cnt, link))
            results.append(link)
            cnt += 1
            if cnt == 11:
                break
        return results
def calculate_spearman(google,ask):
    matched = 0
    sigma_di2 = 0
    glen = len(google)
    alen = len(ask)
    for i in range(0, alen):
        for j in range(0, glen):
            if ask[i] == google[j]:
                matched += 1
                sigma_di2 += (j-i) * (j-i)
    rho = 0
    if matched == 0:
        rho = 0
    elif matched == 1:
        if sigma_di2 == 0:
            rho = 1
        else:
            rho = 0
    else:
        rho = 1-(6*sigma_di2/(matched*(matched*matched-1)))
    return matched, matched*100/glen, rho

# result1 = SearchEngine.search("How is the spinning mule fuelled", False)
googleResultFile = open("./Google_Result3.json")
googleResultJson = json.load(googleResultFile)
googleResultFile.close()

askResultFile = open("./Ask_Result.json")
askResultJson = json.load(askResultFile)
askResultFile.close()

queryFile = open("./100QueriesSet3.txt")
searchWords = queryFile.readline().strip(" \n")
wordCnt = 1

hw1 = open("hw1.csv", "w")
hw1Writer = csv.writer(hw1)

avgA = 0
avgB = 0
avgC = 0

hw1Writer.writerow(["Queries", " Number of Overlapping Results", " Percent Overlap", " Spearman Coefficient"])

while searchWords:
    googleArray = googleResultJson[searchWords]
    askArray = askResultJson[searchWords]
    a, b, c = calculate_spearman(googleArray, askArray)
    hw1Writer.writerow([searchWords, a, b, c])
    avgA += a
    avgB += b
    avgC += c
    print(askArray)
    wordCnt += 1
    searchWords = queryFile.readline().strip(" \n")

print("{},{},{}\n".format(avgA, avgB, avgC))
print("wordCnt : {}\n".format(wordCnt))
hw1Writer.writerow(["Averages", avgA/wordCnt, avgB/wordCnt, avgC/wordCnt])

askResultDict = {}

#
# queryFile = open("./100QueriesSet3.txt")
# searchWords = queryFile.readline().strip(" \n")
# wordCnt = 1
# while searchWords:
#     print("{}:{}".format(wordCnt, searchWords))
#     SearchEngine.search(searchWords, False)
#     wordCnt += 1
#     searchWords = queryFile.readline().strip(" \n")
#
# askResultJson = json.dumps(askResultDict, indent=2)
# askResultFile = open("./Ask_Result.json", "w")
# askResultFile.write(askResultJson)
# askResultFile.close()
