Some scrapers for the USI mods
(okay, scraper. I'm optimistic.)

## To Use
Copy your mods into the working directory, and go.  The scripts expect the GameData directory to be in the same directory as the scripts.

## converters.py
Searches GameData/ for parts which have a Converter module, and outputs them as CSV containing outputs,inputs,process,part.  See example in results directory.

## Known Issues
* If one .cfg file modifies another part, the part's title won't be resolved.  Fixing this is going to take a major re-think, as I currently handle each cfg file atomically, with no state carried between them.
