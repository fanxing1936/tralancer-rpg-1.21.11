# RPG mercenaries return the player's entrusted main-hand item through an authored loot table.
execute if entity @s[tag=rpg.merc] run data modify entity @s DeathLootTable set value "rpg:squad/equipment_return"
# 0f is checked before Looting adjustment in Minecraft 1.21.11 Mob.dropCustomDeathLoot.
data merge entity @s {CanPickUpLoot:0b,drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f,legs:0f,feet:0f,body:0f,saddle:0f}}
tag @s add rpg.drop_policy.v1
