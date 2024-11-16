# POAST
A workflow that works alongside <a href="https://github.com/marketplace/actions/deploy-to-neocities" target="_blank">Deploy to Neocities</a> (although, you can remove this) to also push a new post to Mastodon, *specifically* for Jekyll. This is something I spent ... a very long time working on. There was a time when I stayed up until 2am, got myself 3 hours of sleep, went to work, came home, and then stayed up until 2am again finishing the initial version of **Poast**. Now, with some tweaks, and more tweaks, and a few more tweaks, it works, seamlessly, and without issue.

Welcome, to the **POAST**.

So, how you'll get this to work ...

Firstly, *if you use* Deploy to Neocities, you'll want to have your Neocities API key in a Github secret. But! In order for this workflow to SSH into your VPS (you *NEED* to have a server of some kind in order to make this work), you need to create an SSH key ***without*** a passphrase, and then copy the public key into *another* Github secret. Then, make sure the key is in your authorized_keys file ***on the server*** this script/workflow is connecting to.

Once you've done that, it's SIMPLE.

Put poast.py in /masto-poast/ in whatever directory you're SSH-ing into (you can change this, if you want), and put the neocities.yml into .github/workflows on your Jekyll site.

*Note: I have this running in the root directory, but if you don't want to do that, make a new user!*

NOW, as long as your new posts are formatted /year/month/day/title, and you've *correctly* supplied your blog URL and VPS IP to the YML, and *as long as* your new posts go to _posts on your site, AND as long as you setup BOTH of those keys, and supplied poast.py with your instance URL (there are clearly marked sections in both scripts that depict where you should put these things) ...

*Also note: Make sure you make an environment for the script and then run:
```
pip install requests beautifulsoup
```
This will post new Jekyll blog posts directly to Mastodon, by reading the current day and *only* posting blog posts ***from said date*** (I've done this in order to avoid spam, which I have done, by accident, multiple times).

Included in poast.py is a field to customize just exactly *what* the post says once it's posted to your instance. Mine says, "Posted via Nova Prime: (url)" and then supplies a hashtag derived from my tags I'm using on Jekyll. You should *also* set that up, so that your posts can categorize themselves upon posting to Mastodon. But that's easy enough to setup.

Make a "tag" folder on your Jekyll site. Make new .md files with the names of tags you frequently or want to use, and include this in the front matter:
```
---
layout: tagpage
title: "Tag: scripting"
tag: scripting
---
```
(the tag "scripting" is just an example, change these two lines to whatever your tag name is)

Then, put a tagpage in _layouts:
```
---
layout: default
---
<div id="main">
  <table>
    <tr>
    <td>


<a class="read-title" href="/">Tag: {{ page.tag }}</a>
<br />
<ul>
{% for post in site.tags[page.tag] %}
  <li><a href="{{ post.url }}">{{ post.title }}</a> ({{ post.date |     date_to_string }})<br>
    {{ post.description }}
  </li>
{% endfor %}
</ul>
</div>


{% include archive.html %}

  </td>
  </tr>
  </table>

</div>
```
Then, put an archive.html and collecttags.html in your _includes.

archive.html:
```

<p><em>custom text for whatever you want to type at the top of your archive page</em></p>

<p class="cloud">
{% capture temptags %}
  {% for tag in site.tags %}
    {{ tag[1].size | plus: 1000 }}#{{ tag[0] }}#{{ tag[1].size }}
  {% endfor %}
{% endcapture %}
{% assign sortedtemptags = temptags | split:' ' | sort | reverse %}
{% for temptag in sortedtemptags %}
  {% assign tagitems = temptag | split: '#' %}
  {% capture tagname %}{{ tagitems[1] }}{% endcapture %}
  <a href="/tag/{{ tagname }}"><code class="highligher"><nobr>{{ tagname    }}</nobr></code></a>
{% endfor %}
</p>
```

collecttags.html
```
{% assign rawtags = "" %}
{% for post in site.posts %}
  {% assign ttags = post.tags | join:'|' | append:'|' %}
  {% assign rawtags = rawtags | append:ttags %}
{% endfor %}
{% assign rawtags = rawtags | split:'|' | sort %}

{% assign site.tags = "" %}
{% for tag in rawtags %}
  {% if tag != "" %}
    {% if tags == "" %}
      {% assign tags = tag | split:'|' %}
    {% endif %}
    {% unless tags contains tag %}
      {% assign tags = tags | join:'|' | append:'|' | append:tag | split:'|' %}
    {% endunless %}
  {% endif %}
{% endfor %}
```
Then, in the "head" document (which you should have as head.html in the _includes directory), add this:
```
{% if site.tags != "" %}
    {% include collecttags.html %}
  {% endif %}
```
Boom, now you can put tags onto your posts, and **POAST** will use these as hashtags once posted to Mastodon.

You should *also* note that poast.py is currently looking into div class "indent" in order to extract the first < p > tag (i.e., the first paragraph of your post) for a summary. You *likely* won't be using a div class called "indent" to wrap around your posts, so change this to whatever div class contains your posts!
```
    # Extract the first <p> tag within the .indent div as a summary
    indent_div = soup.find('div', {'class': 'indent'})
    if indent_div:
        paragraphs = indent_div.find_all('p')
        summary = paragraphs[0].get_text() if paragraphs else "No summary available"
    else:
        summary = "No summary available"
```

***VOILA!***

Once you've made a post, I would suggest watching the workflow in-action on Github to make sure it's functioning properly. There *should* be sufficient debugging attached to these scripts to figure out what's going wrong, *if anything goes wrong*.

Enjoy.
