#!/usr/bin/env python
# coding: utf-8

# In[1]:


# source 1: https://stackoverflow.com/questions/596216/formula-to-determine-perceived-brightness-of-rgb-color
# source 2: https://stackoverflow.com/questions/6442118/python-measuring-pixel-brightness


# In[6]:


def get_fazarticles(to, fr):
    
    import time, os
    links = []
    source = []
    title = []
    heading = []
    publishtime = []
    labelpaid = []
    author = []

    chromedriver = "/media/fabian/VM_space/Metis/02_Regression/chrome_driver/chromedriver" # path to the chromedriver executable
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)

    faz_newsticker_url = 'https://www.faz.net/faz-live-p1'
    driver.get(faz_newsticker_url)

    time.sleep(1)
    driver.switch_to.frame('sp_message_iframe_660749')
    consent_picker = driver.find_element_by_xpath('//*[@id="notice"]/div[4]/div[1]/button[2]')
    consent_picker.click()

    for i in range(int((pd.to_datetime(to) - pd.to_datetime(fr)).days)+1):
        d = pd.to_datetime(to) - timedelta(days=i)
        date_scrape1 = str(pd.to_datetime(d).month)
        date_scrape2 = str(pd.to_datetime(d).day)
        date_scrape3 = str(pd.to_datetime(d).year)


        for i in range(1, 15):
            faz_newsticker_url = 'https://www.faz.net/faz-live-p' + str(i)
            driver.get(faz_newsticker_url)

            date_picker = driver.find_element_by_xpath('//*[@id="from"]')
            date_picker.send_keys(Keys.ARROW_LEFT)
            date_picker.send_keys(Keys.ARROW_LEFT)
            if len(date_scrape1) == 1:
                date_picker.send_keys('0'+date_scrape1)
            else:
                date_picker.send_keys(date_scrape1)
            if len(date_scrape2) == 1:
                date_picker.send_keys('0'+date_scrape2)
            else:
                date_picker.send_keys(date_scrape2)
            date_picker.send_keys(date_scrape3)
            
            date_picker = driver.find_element_by_xpath('//*[@id="till"]')
            date_picker.send_keys(Keys.ARROW_LEFT)
            date_picker.send_keys(Keys.ARROW_LEFT)
            
            if len(date_scrape1) == 1:
                date_picker.send_keys('0'+date_scrape1)
            else:
                date_picker.send_keys(date_scrape1)
            if len(date_scrape2) == 1:
                date_picker.send_keys('0'+date_scrape2)
            else:
                date_picker.send_keys(date_scrape2)
            date_picker.send_keys(date_scrape3)

            apply_button = driver.find_element_by_xpath('//*[@id="contentHeaderFooter"]/div[1]/div/div/form/div[2]/div[3]/button')
            apply_button.click()
            time.sleep(1)

            soup = bs(driver.page_source)

            for i in soup.find_all(class_='ticker-news-item'):
                if i.find('a')['href'] != None:
                    links.append(i.find('a')['href'])
                else:
                    links.append('no_link')

            for i in soup.find_all(class_='ticker-news-item'):
                if i.find(class_='ticker-news-type').find('img')['alt'] != None:
                    source.append(i.find(class_='ticker-news-type').find('img')['alt'])
                else:
                    source.append('no_info')

            for i in soup.find_all(class_='ticker-news-text'):
                if i.find('a').text != None:
                    title.append(i.find('a').text.strip())
                else:
                    title.append('no_info')

            for i in soup.find_all(class_='ticker-news-text'):
                try:
                    heading.append(i.find(class_='ticker-news-super').text.strip().replace(' :', ''))
                except:
                    heading.append('no_info')

            for i in soup.find_all(class_='ticker-news-item'):
                if i.find('time').text != None:
                    publishtime.append(i.find('time').text)
                else:
                    publishtime.append('no_info')

            for i in soup.find_all(class_='ticker-news-item'):
                if i.find(class_='ticker-news-type').find('img')['alt'] == 'FAZ+':
                    labelpaid.append(True)
                else:
                    labelpaid.append(False)

            for i in soup.find_all(class_='ticker-news-item'):
                try:
                    author.append(i.find(class_='ticker-news-author').text)
                except:
                    author.append('no_info')

    df_faz = pd.DataFrame({
        'links': links,
        'source': source,
        'title': title,
        'heading': heading,
        'publishtime': publishtime,
        'labelpaid':labelpaid,
        'author': author
    })

    df_faz.drop_duplicates(inplace=True)
    df_faz.reset_index(drop=True, inplace=True)
    
    driver.quit()

    return(df_faz)


# In[15]:


def get_faz_meta(fazarticles_df):
    
    image_meta = []
    labelpaid_meta = []
    opinion_meta = []
    author_meta = []
    readtime_meta = []
    source_meta = []
    keywords_meta = []
    
    for i in range(len(fazarticles_df['links'])):
        url = fazarticles_df['links'][i]
        
        try:
            response = requests.get(url)
        except:
            try:
                response = requests.get(url)
            except:
                response = requests.get(url)
        page = response.text
        soup = bs(page)
    
        try:
            image_meta.append(soup.find('meta', {'property': 'og:image'})['content'])
        except:
            image_meta.append('no_info')
        
        try:
            labelpaid_meta.append(str(soup.find_all('script')).find('window.isPaidContent = true') > 1)
        except:
            labelpaid_meta.append('no_info')
        
        try:
            opinion_meta.append(soup.find(class_= 'atc-MetaAuthorText').text.strip())
        except:
            opinion_meta.append('no_info')
        
        try:
            author_meta.append(soup.find(class_= 'atc-MetaAuthor').text.strip())
        except:
            author_meta.append('no_info')
        
        try:
            readtime_meta.append(soup.find(class_= 'atc-ReadTime_Text').text.strip())
        except:
            readtime_meta.append('no_readtime_shown')
        
        try:
            source_meta.append(str(soup.find_all('script'))[str(soup.find_all('script')).find('"source"')+10:str(soup.find_all('script')).find('"source"')+30])
        except:
            source_meta.append('no_info')
            
            
        try:
            keywords_meta.append(soup.find('meta', attrs={'name':"keywords"}).attrs['content'])
        except:
            keywords_meta.append('no_info')
            

        print(f'Article number {i} scraping completed.')
            
    df_meta_temp = pd.DataFrame({
        'image_meta': image_meta,
        'labelpaid_meta': labelpaid_meta,
        'opinion_meta': opinion_meta,
        'author_meta': author_meta,
        'readtime_meta': readtime_meta,
        'source_meta': source_meta,
        'keywords_meta': keywords_meta
    })
            
    return(df_meta_temp)


# In[7]:


def get_image_brightness(image_list):
    global bright_list
    bright_list = []
    for i, j in enumerate(image_list):
        try:
            imag = Image.open(urlopen(j))
            #Convert the image te RGB if it is a .gif for example
            imag = imag.convert ('RGB')
            #coordinates of the pixel
            X,Y = 0,0
            #Get RGB
            pixelRGB = imag.getpixel((X,Y))
            R,G,B = pixelRGB 

            brightness = (0.2126*R) + (0.7152*G) + (0.0722*B)
            bright_list.append(brightness)
        except:
            bright_list.append(np.nan)
        print(i)
    return(bright_list)

def get_dominant_color(image_list):
    colors = ['red', 'green', 'blue']
    global color_list
    color_list = []
    for i, j in enumerate(image_list):
        try:
            imag = Image.open(urlopen(j))
            #Convert the image te RGB if it is a .gif for example
            imag = imag.convert ('RGB')
            #coordinates of the pixel
            X,Y = 0,0
            #Get RGB
            pixelRGB = imag.getpixel((X,Y))
            R,G,B = pixelRGB 

            dominant_color = colors[np.argmax([R, G, B])]
            color_list.append(dominant_color)
        except:
            color_list.append(np.nan)
        print(i)
    return(color_list)


# In[8]:


def get_fazmeta_not_paid(fazarticles_df):
    
    image_meta = []
    labelpaid_meta = []
    opinion_meta = []
    author_meta = []
    readtime_meta = []
    source_meta = []
    keywords_meta = []
    
    for i in range(len(fazarticles_df)):
        url = fazarticles_df[i]
        
        try:
            response = requests.get(url)
        except:
            try:
                response = requests.get(url)
            except:
                response = requests.get(url)
        page = response.text
        soup = bs(page)
    
        try:
            image_meta.append(soup.find('meta', {'property': 'og:image'})['content'])
        except:
            image_meta.append('no_info')
        
        try:
            labelpaid_meta.append(str(soup.find_all('script')).find('window.isPaidContent = true') > 1)
        except:
            labelpaid_meta.append('no_info')
        
        try:
            opinion_meta.append(soup.find(class_= 'atc-MetaAuthorText').text.strip())
        except:
            opinion_meta.append('no_info')
        
        try:
            author_meta.append(soup.find(class_= 'atc-MetaAuthor').text.strip())
        except:
            author_meta.append('no_info')
        
        try:
            readtime_meta.append(soup.find(class_= 'atc-ReadTime_Text').text.strip())
        except:
            readtime_meta.append('no_readtime_shown')
        
        try:
            source_meta.append(str(soup.find_all('script'))[str(soup.find_all('script')).find('"source"')+10:str(soup.find_all('script')).find('"source"')+30])
        except:
            source_meta.append('no_info')
            
            
        try:
            keywords_meta.append(soup.find('meta', attrs={'name':"keywords"}).attrs['content'])
        except:
            keywords_meta.append('no_info')
            

        print(f'Article number {i} scraping completed.')
            
    df_meta_temp = pd.DataFrame({
        'image_meta': image_meta,
        'labelpaid_meta': labelpaid_meta,
        'opinion_meta': opinion_meta,
        'author_meta': author_meta,
        'readtime_meta': readtime_meta,
        'source_meta': source_meta,
        'keywords_meta': keywords_meta
    })
            
    return(df_meta_temp)


# In[9]:


def get_fazmeta_paid(fazarticles_df, headers, cookies):
    x = 0
    source = []
    teaser = []
    read_time_min = []
    sharings = []
    opinions = []
    author_disp = []
    author_link_personal_site = []
    text_full = []
    paragraphs_full = []
    page_no = []

    articles_paid_total = len(fazarticles_df)

    for i in fazarticles_df:
        url = i + '?premium'
        response = requests.get(url, headers=headers, cookies=cookies)
        page = response.text
        soup = bs(page)

        try:
            source.append(soup.find(class_="atc-Footer_Quelle").text.replace('Quelle: ', '').replace('(', '').replace(')', ''))
        except:
            try:
                url_2 = url[:url.find('html')-1] + '-p2' + url[url.find('html')-1:]
                response_2 = requests.get(url_2)
                page_2 = response_2.text
                soup_2 = bs(page_2)
                source.append(soup_2.find(class_="atc-Footer_Quelle").text.replace('Quelle: ', '').replace('(', '').replace(')', ''))
            except:
                try:
                    url_3 = url[:url.find('html')-1] + '-p3' + url[url.find('html')-1:]
                    response_3 = requests.get(url_3)
                    page_3 = response_3.text
                    soup_3 = bs(page_3)
                    source.append(soup_3.find(class_="atc-Footer_Quelle").text.replace('Quelle: ', '').replace('(', '').replace(')', ''))
                except:
                    try:
                        url_4 = url[:url.find('html')-1] + '-p4' + url[url.find('html')-1:]
                        response_4 = requests.get(url_4)
                        page_4 = response_4.text
                        soup_4 = bs(page_4)
                        source.append(soup_4.find(class_="atc-Footer_Quelle").text.replace('Quelle: ', '').replace('(', '').replace(')', ''))
                    except:
                        try:
                            url_5 = url[:url.find('html')-1] + '-p5' + url[url.find('html')-1:]
                            response_5 = requests.get(url_5)
                            page_5 = response_5.text
                            soup_5 = bs(page_5)
                            source.append(soup_4.find(class_="atc-Footer_Quelle").text.replace('Quelle: ', '').replace('(', '').replace(')', ''))
                        except:
                            source.append('na')


        try:
            teaser.append(soup.find(class_='atc-IntroText').text.replace('\n', '').replace('\t', ''))
        except:
            teaser.append('na')

        try:
            read_time_min.append(soup.find(class_="atc-ReadTime_Text").text.replace(' Min.', ''))
        except:
            read_time_min.append('na')

        try:
            sharings.append(soup.find(class_="ctn-PageFunctions_List js-sharebuttons")['data-empfehlen-value'])
        except:
            sharings.append('na')

        try:
            opinions.append(soup.find(class_="ctn-PageFunctions_List js-sharebuttons")['data-comment-value'])
        except:
            opinions.append('na')

        try:
            author_disp.append(soup.find(class_="Content Autor caps").text)
        except:
            author_disp.append('na')

        try:
            author_link_personal_site.append(soup.find(class_="aut-Teaser_Name")['title'])
        except:
            author_link_personal_site.append('na')

        try:
            page_no.append(soup.find_all(class_="nvg-Paginator_Item nvg-Paginator_Item-page-number")[-1].text.replace('\n', '').strip())
            page_no_temp = soup.find_all(class_="nvg-Paginator_Item nvg-Paginator_Item-page-number")[-1].text.replace('\n', '').strip()
        except:
            page_no.append('1')
            page_no_temp = 1

        paragraphs = 0
        text = ''
        for j in soup.find_all(class_="atc-TextParagraph"):
            paragraphs += 1
            text += ' '+ j.text
            text = text.lstrip()

        try:
            if int(page_no_temp) > 1:
                url_2 = url[:url.find('html')-1] + '-p2' + url[url.find('html')-1:]
                response_2 = requests.get(url_2)
                page_2 = response_2.text
                soup_2 = bs(page_2)

                for k in soup_2.find_all(class_="atc-TextParagraph"):
                    paragraphs += 1
                    text += ' '+ k.text
                    text = text.lstrip()

            if int(page_no_temp) > 2:
                url_3 = url[:url.find('html')-1] + '-p3' + url[url.find('html')-1:]
                response_3 = requests.get(url_3)
                page_3 = response_3.text
                soup_3 = bs(page_3)

                for k in soup_3.find_all(class_="atc-TextParagraph"):
                    paragraphs += 1
                    text += ' '+ k.text
                    text = text.lstrip()

            if int(page_no_temp) > 3:
                url_4 = url[:url.find('html')-1] + '-p4' + url[url.find('html')-1:]
                response_3 = requests.get(url_4)
                page_4 = response_4.text
                soup_4 = bs(page_4)

                for k in soup_4.find_all(class_="atc-TextParagraph"):
                    paragraphs += 1
                    text += ' '+ k.text
                    text = text.lstrip()

            if int(page_no_temp) > 4:
                url_5 = url[:url.find('html')-1] + '-p5' + url[url.find('html')-1:]
                response_5 = requests.get(url_5)
                page_5 = response_5.text
                soup_5 = bs(page_5)

                for k in soup_5.find_all(class_="atc-TextParagraph"):
                    paragraphs += 1
                    text += ' '+ k.text
                    text = text.lstrip()

        except:
            None
        text_full.append(text)
        paragraphs_full.append(paragraphs)

        x += 1
        print(f'Scraping completed for {x} of {articles_paid_total} articles.')
    return(source, 
           teaser, 
           read_time_min, 
           sharings,
           opinions,
           author_disp,
           author_link_personal_site,
           text_full,
           paragraphs_full,
           page_no)


# In[ ]:





# In[ ]:





# In[ ]:




