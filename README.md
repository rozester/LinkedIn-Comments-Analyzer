# LinkedIn Comment Analyzer

Extracting LinkedIn comments from any post and export it to Excel file

1- Expand all comments and replies from linkedin post, 
    by clicking all "Show previous comments" until all comments are visible

2- Expand all comment replies by clicking all "Load previous replies" until all replies are visible

3- Press F12 in your browser and select all comments with the parent div it must be like this example:-

```
<div id="ember1482" class="feed-base-comments-list feed-base-comments-list--expanded ember-view"><!---->
<!---->
      <article>
      <article>
      <article>
      
      ....
      
      <article>
<div>
```

4- Right click on that div and then press "Edit As HTML" and copy all contents

5- Save these contents in a text file "Comments.html" and make sure that encoding is UTF-8

6- Put this file inside the same directory with this python file "linkedin-comments-grabber.py"

7- Excute linkedin-comments-grabber.py
