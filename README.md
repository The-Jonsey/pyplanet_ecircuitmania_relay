# PyPlanet eCircuitMania Relay

## A PyPlanet plugin to send live match results to eCircuitmania


### How to start

the command `//ecm start {token}` will start the plugin sending round results to eCircuitmania, the format of the token is the matchId and the token, with an underscore separating them (most likely how eCircuitmania provided it) e.g `//ecm start 1730289600000x001_5YFH3QF2`


### How to stop

the command `//ecm stop` will clear the matchId and token, which will stop the match data being sent to eCircuitmania

If the plugin detects the match ends, or a new script gets loaded, it will auto disconnect, and you will need to restart by calling the start command again

### Chat messages

The plugin will post serveral types of messages in chat on certain conditions, these being:
- `E-Circuitmania connection activated` on the start command being called, with a valid token
- `E-Circuitmania connection closed` on any of the causes for the plugin to stop (stop command called, new script loaded, match ended)
- `Error with connection to ECM, data-loss may occur` on an unexpected response from eCircuitmania, this may suggest any backup methods for storing the match results should be ready