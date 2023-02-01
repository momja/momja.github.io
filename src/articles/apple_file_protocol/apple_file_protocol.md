---
title: "Earth 🪐 to Localhost"
description: "Setting up a NAS with Apple Filing Protocol"
publish_date: 2023-01-31
---

# Earth 🪐 to Localhost...

This is the first note I've written on my locally-hosted network attached storage setup. This is currently running on the [Apple Filing Protocol](https://en.wikipedia.org/wiki/Apple_Filing_Protocol). This is possible thanks to the reimplementation of the AFP protocol by the [Netatalk](https://netatalk.sourceforge.io/) project, which is a "free and open source AFP fileserver."

AFP I guess is deprecated on Mac's, so they cannot _serve_ data via AFP, but they can still login to other networks running the protocol. I'm running this on my raspberry pi, which is awfully slow, but who cares? Once it's loaded, it's loaded. I've got access to my files, and they are mostly text, so it really doesn't matter.

There is a problem though. The iOS files app does _not_ support the AFP protocol. Even though it's Apple's own protocol, as far as I can tell, it _was_ never supported on mobile. So next step for me will be converting my notes file server to the Server Message Block (SMB) protocol. This was originally created by Microsoft, but an implementation called [Samba](https://ubuntu.com/server/docs/samba-file-server) allows Unix-like devices to interface with Windows, and other Unix-like devices. Pretty neat! I don't use Window often, but I do have a PC, so I'd like it to be supported.

## An aside...
Today is also the last day of January. One month down in 2023!
