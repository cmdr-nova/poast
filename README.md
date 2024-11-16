# POAST
A workflow that works alongside <a href="https://github.com/marketplace/actions/deploy-to-neocities" target="_blank">Deploy to Neocities</a> (although, you can remove this) to also push a new post to Mastodon, *specifically* for Jekyll. This is something I spent ... a very long time working on. There was a time when I stayed up until 2am, go myself 3 hours of sleep, went to work, came home, and then stayed up until 2am again finishing the initial version of **Poast**. Now, with some tweaks, and more tweaks, and a few more tweaks, it works, seamlessly, and without issue.

Welcome, to the **POAST**.

So, how you'll get this to work ...

Firstly, *if you use* Deploy to Neocities, you'll want to have your Neocities API key in a Github secret. But! In order for this workflow to SSH into your VPS (you *NEED* to have a server of some kind in order to make this work), you need to create an SSH key ***without*** a passphrase, and then copy the public key into *another* Github secret. Then, make sure the key is in your authorized_keys file ***on the server*** this script/workflow is connecting to.

Once you've done that, it's SIMPLE.

Put poast.py in /masto-poast/ in whatever directory you're SSH-ing into (you can change this, if you want), and put the neocities.yml into .github/workflows on your Jekyll site.

NOW, as long as your new posts are formatted /year/month/day/title, and you've *correctly* supplied your blog URL to the YML, and *as long as* your new posts go to _posts on your site, AND as long as you setup BOTH of those keys, and supplied poast.py with your instance URL ...

This will post new Jekyll blog posts directly to Mastodon, by reading the current day and *only* posting blog posts ***from said date*** (I've done this in order to avoid spam, which I have done, by accident, multiple times).
