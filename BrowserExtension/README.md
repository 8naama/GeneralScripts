# Support browser extension for unassigned chats
This browser extension sends a GET request to a [Logz Support Endpoint](https://github.com/logzio/support-internal/blob/master/SpikeTheDog/Dev/spikeTheDog.py#L436), to find out if there are unassigned chats in the Intercom unassigned queue.
Upon finding an unassign chat, the tab logo and name changes and the Intercom dark mode gets toggled on and off.

## Prerequisites
You will need Chrome browser in version that supports Manifest version 3.

## Setup
1. Download and save the extension folder locally. 
2. Open Chrome manage [extensions page](chrome://extensions/)
3. Enable Developer mode from the top right
4. Click "Load unpacked" and choose the path in your PC where you saved the browser extension folder.
