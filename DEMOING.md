# How to use this app to demonstrate Segment

Segment is a tough tool to demonstrate because it's 'plumbing'... that is, nobody wants to just watch Segment do its thing, they experience its magic indirectly, by using other tools that are integrated with it, and seeing the results.

The purpose of Seg-Mart is to give a quick place for someone to play that can easily be plugged in to show how Segment helps you.  To do this, I've provided a bit of a storytelling guide below so that you can see how it might be of interest to a customer.

## The Status Quo

You have a website, right?  People come to it, browse things, click buttons, and move on.  They cause some compute to occur, maybe raise the price of your cloud bill, and then don't end up buying.  Why?  Well, as things stand, it's hard to know anything about them.  One of two things is true:

1- You have no technology gathering any sort of data for your marketing team to use.  They're relying on other channels to reach out to customers.  Your website, the most likely interaction point with your customers, is a completely untapped resource in your quest for knowledge.

2- You have some tools but they're cumbersome to maintain.  Every time someone wants something piped to another tool, there's a big developer effort and lots of arguing over the quality of the resulting data, because Tool A and Tool B and Tool C all present completely different stories that don't seem to provide any consistency.

## The Hero's Journey

The hero of this story is YOU, the developer.  See, the problem we're trying to solve is that we need to learn more about our customers, but it's hard to get to know someone who browses your website... because there's no interaction with them!

So let's follow Jeff around your store and see what he gets into...

**At this point in the demo, you can play the game from the main branch.  You're just watching someone do stuff, click buttons, have fun exploring the store.**

So imagine that this store is actually your website.  You're watching Jeff navigate the links from page to page, and trying to figure him out.  That's cool, but you can't afford to pay someone to watch each session.  You might have 10,000 customers today from all over the world... it's just not cost-effective.

This is why Segment is important.  Let's implement it with our store...

### Pre-work
* Create a file in /config/ called `env_vars.py`
* In the file, make a variable `SEGMENT_WRITE_KEY = xxxxxx`, replacing the x's with the write key from your Python Segment Source.
* Save it, don't open the file during the demo so you don't leak your key!

### Demo Steps
1. In our store, you provide your email address to enter.  Think of this as your website's "login" page... after which the user is identified.
1. We're going to inject Segment first into this process, because it's important that we establish the identity of a visitor.

Go to `app/views/` and look for `title_screen.py`.
1. Add `import segment.analytics as analytics` at the top of the file.
1. Just below it, add `from config.env_vars.py import SEGMENT_WRITE_KEY`
1. In the `__init__` method, add a line to establish the write key: `analytics.write_key = SEGMENT_WRITE_KEY`
1. Look down where the identity is established (about line 38), and add your Segment identify() call: `analytics.identify(config.globalvars.identity)`

Go to `app/modules/` and look for `player.py`.
1. Add `import segment.analytics as analytics` at the top of the file.
1. Just below it, add `from config.env_vars.py import SEGMENT_WRITE_KEY`
1. In the `__init__` method, add a line to establish the write key: `analytics.write_key = SEGMENT_WRITE_KEY`
1. Look for the "Object interaction controls" - you'll add a track() on line 73-ish:  `analytics.track(config.globalvars.identity, 'Added Item to Cart', {'item_id': config.globalvars.object_interaction})`

Go to `app/modules` and look for `ui.py`.
1. Add `import segment.analytics as analytics` at the top of the file.
1. Just below it, add `from config.env_vars.py import SEGMENT_WRITE_KEY`
1. In the `__init__` method, add a line to establish the write key: `analytics.write_key = SEGMENT_WRITE_KEY`
1. Look for the shopping_bag.clear() call around line 80.  You'll add a track() right next to this: `analytics.track(config.globalvars.identity, 'Cleared Shopping Cart')`

Now let's revisit Jeff wandering around our store.  (Restart the application, but also have the Segment debugger up on the screen too).  As Jeff adds various items to his bag, or maybe clears the cart out... Segment gathers those events so that we know what Jeff's up to.

Imagine we had more time to implement - what other events would we want to track?  Maybe when Jeff...
* enters various sections of the store
* checks out
* uses a coupon
* uses an in-store ATM
* puts items on his Wish List

If we can identify an event in the code, we can ask Segment to track it, with the identity of our customer along for the ride... and we can push that data to any tool in our stack that needs to know it.  Suddenly, we can build instant context around our customers, even at the scale that our website brings in!