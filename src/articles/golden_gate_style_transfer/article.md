---
title: "Using Style Transfer and CNC to Produce Printblocks"
description: "A new way to make prints"
publish_date: 2025-01-03
tags: [styleTransfer, 100DaysToOffload, blog]
---

# Using Style Transfer to CNC Produce Printblocks

In college, I wrote a final paper about [Generative Adversarial Nets for Artistic Image-to-Image Translation](https://dizzard.net/images/Final__CycleGAN_on_Image_Transfer.pdf) where I explored how GANs can be used for image style transfer. In my experiments, I never got great results.

![../images/gan_example.png](../../images/gan_example.png)

That college paper was much more down in the dirt with the model than what I've tried recently. For an event, I needed to create a bunch of printmaking blocks very quickly, and they needed to be centered around San Francisco Landmarks. To accomplish this, I took a look at diffusion models. Using Dall-E 3, I was able to apply a woodblock print style transfer, and with some further processing, I could vectorize the output and send it to a CNC machine to manufacture the stamp. In the example below, it shows the original public domain image, the result of style transfer on the image, then the linoleum block, and the final print.

![](../../images/golden_gate_process.png)

## The Tools
I used OpenAI's ChatGPT interface to apply style transfer (I know, this is not to be confused with "Neural Style Transfer" which is a specific set of algorithms) There was quite a bit of clean up in Gimp, then Inkscape to remove blurry lines, clean up the fog. The stamp was carved on a Nomad 3 CNC with a 90º Vee Bit, with further cleanup by hand with some carving tools.

