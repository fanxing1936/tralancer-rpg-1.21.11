execute unless data storage rpg:say t[0] run return 0
data modify storage rpg:say e set from storage rpg:say t[0]
data remove storage rpg:say t[0]
execute store result score #due rpg_say run data get storage rpg:say e.due
execute if score #due rpg_say > #now rpg_say run data modify storage rpg:say q append from storage rpg:say e
execute if score #due rpg_say <= #now rpg_say run function rpg:town/say/fire with storage rpg:say e
function rpg:town/say/each
