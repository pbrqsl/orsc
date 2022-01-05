from bs4 import BeautifulSoup
import requests
import json
import time
import asyncio
import aiohttp

async def scrap_multiple_pages(loop, *urls):
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(scrap_page(session, url))
            tasks.append(task)
        all_tasks = asyncio.gather(*tasks)
        return await all_tasks

async def scrap_page(session, url):
    page_start = time.time()
    async with session.get(url) as response:
        print(f'{url}')
        print(f'Page took: {time.time() - page_start}')
        return await response.text()

def urls_by_id(course_id: str):
    search_url = f'https://learning.oreilly.com/api/v2/search/?query={course_id}'
    page = requests.get(search_url).content
    soup = BeautifulSoup(page, 'html.parser')
    search_dict = json.loads(soup.text)
    for result in search_dict['results']:
        course_page = requests.get(result['url']).content
        course_soup = BeautifulSoup(course_page, 'html.parser')
        course_dict = json.loads(course_soup.text)
        course_chapters = course_dict['chapters']
        course_url = course_dict['web_url']
        course_title = course_dict['title']
        base = course_url
        or_base = base.split("/library/")[0]
        course_name = base.split("/view/")[1][:-1]
        course_number = base.split('/')[-2]
        loop1 = asyncio.new_event_loop()
        asyncio.set_event_loop(loop1)
        results = loop1.run_until_complete(scrap_multiple_pages(loop1, *course_chapters))
        chapters_dict = {}
        print(loop1.is_closed())
        for result in results:
            chapter_soup = BeautifulSoup(result, 'html.parser')
            chapter_dict = json.loads(chapter_soup.text)
            url = chapter_dict['url']
            descrition = chapter_dict['description']
            chapters_dict[url] = descrition
        links = []
        for chapter in course_chapters:
            video_id = chapter.split('/')[-1].split('.html')[0]
            vid_url = f'{or_base}/videos/{course_name}/{course_number}-{video_id}'
            vid_title = chapters_dict[chapter]
            links.append([vid_title, vid_url])
        return [course_title, links]


if __name__ == '__main__':
    print(urls_by_id('9780133929171'))
