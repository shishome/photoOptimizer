# photoOptomizer

Quick python script utilizing PhotoScript to identify and tag duplicates in a Photo Library.

## How to use
1. Clone the repo
2. Install requirements listed in requirements.txt
3. Set the number of photos + videos in your Photos.app library to the variable in .env (Or set PHOTO_LIB_COUNT in your env manually.)
4. Run the script and be patient. Photos will ask you for permission to automate, allow it.

## Tips
* Run this script in a terminal, do not run it in an IDE or it will try to use the IDE's entitlements, which dont usually include access to the Photos DB
* Don't close the Terminal or Photos Apps while this process is ongoing, as it will error out.
* Don't change the pagination to anything higher than 10 per AppleScript query. Once you start getting into the 10k number of items it can start to time out if its any higher than that.