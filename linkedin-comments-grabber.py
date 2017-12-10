"""
LinkedIn Comments Analyzer

Copyright 2017 Amr Salama
Twitter: @amr_salama3
Github: rozester/LinkedInCommentAnalyzer

MIT License

Work Steps:-

1- Expand all comments and replies from linkedin post, 
    by clicking all "Show previous comments" until all comments are visible

2- Expand all comment replies by clicking all "Load previous replies" until all replies are visible

3- press f12 in your browser and select all comments with parent div it must be like this example:-

<div id="ember1482" class="feed-base-comments-list feed-base-comments-list--expanded ember-view"><!---->
<!---->
      <article>
      <article>
      <article>
      
      ....
      
      <article>
<div>

4- right click on that div and then press "Edit As HTML" and copy all contents

5- save these contents in a text file for example Comments.html and make sure that encoding is UTF-8

Enjoy Data Science :)
"""

import pandas as pd
from bs4 import BeautifulSoup

# the file which contains all comments
file = open('Comments.html', 'r',encoding='utf8')
html_doc = file.read()
file.close()

# Parse html file
soup = BeautifulSoup(html_doc, 'html.parser')

# Select all comments and replies html tags
comments = soup.div.find_all("article", recursive=False)

# Prepare Dataframe for loading all comments and replies inside it
output_comments_df = pd.DataFrame(columns=['CommentID', 'ParentID', 'LinkedIn ID', 'Name', 'Photo', 
                                           'Comment', 'Likes', 'Replies'])

# Data Cleansing Phase
def paragraph_cleaning(p):
    # Normal Comment
    if (p.span and p.span.span):
        return p.span.span.string.replace('\n','').strip()

#    # mention comment
#    elif (p.span and p.span.a):
#        return p.span.a.string.replace('\n','').strip()
#    elif (p.a.span):
#        return p.a.span.string.replace('\n','').strip()
#    # url comment
#    elif (cmnt.find('p').a):
#        return cmnt.find('p').a.string.replace('\n','').strip()
#    return p
        
    # Complicated Comment
    p_body = ""
    for cmnt in p.children:
        if (cmnt.string):
            p_body = p_body + cmnt.string
        else:
            p_body = p_body + " " + cmnt.a.string
    return p_body

def get_likes(comment):
    # likes exists
    likes = comment.find('button', class_="feed-base-comment-social-bar__likes-count Sans-13px-black-55% hoverable-link-text")
    if (likes):
        return likes.span.string.split(" ")[0]
    return 0

def get_replies(comment):
    # replies exists
    replies = comment.find('button', class_="feed-base-comment-social-bar__comments-count Sans-13px-black-55% hoverable-link-text")
    if (replies):
        return replies.span.string.split(" ")[0]
    return 0

i = 0
# Fill Dataframe with comments and replies
def add_comment(parent, comment):
    global i
    output_comments_df.loc[i] = \
        [
            i + 1, 
            parent, 
            comment.a.attrs.get('href'), 
            comment.find('span', 
                class_="feed-base-comment-item__name Sans-13px-black-70%-semibold").
                string.replace('\n','').strip(), 
            comment.img.attrs.get('src'),
            paragraph_cleaning(comment.find('p')), 
            get_likes(comment), 
            get_replies(comment)
        ]
    i = i + 1
    return i

# Get all replies
def add_comment_replies(parent, comment):
    if (comment.article):
        for cmnt in comment.find_all("article"):
            add_comment(parent, cmnt)

# the main iterator for all comments and replies
for cmnt in comments:
    cmnt_id = add_comment(0, cmnt)
    add_comment_replies(cmnt_id, cmnt)

# Fixing Data Types
output_comments_df['CommentID'] = output_comments_df['CommentID'].astype(int)
output_comments_df['ParentID'] = output_comments_df['ParentID'].astype(int)
output_comments_df['Likes'] = output_comments_df['Likes'].astype(int)
output_comments_df['Replies'] = output_comments_df['Replies'].astype(int)

# Exporting to Excel file
writer = pd.ExcelWriter('output.xlsx')
output_comments_df.to_excel(writer,'Sheet1')
writer.save()
