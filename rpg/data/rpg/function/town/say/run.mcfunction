execute store result score #now rpg_say run time query gametime
data modify storage rpg:say t set from storage rpg:say q
data modify storage rpg:say q set value []
function rpg:town/say/each
