particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1 force
particle minecraft:flame ~ ~0.5 ~ 2 0.5 2 0.1 120 force
playsound minecraft:entity.generic.explode master @a[distance=..64] ~ ~ ~ 2 0.6
summon minecraft:block_display ~-0.5 ~ ~-0.5 {Tags:["rpg.ev.deco"],block_state:{Name:"minecraft:crying_obsidian"},brightness:{sky:15,block:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~0.1 ~0.6 ~0.1 {Tags:["rpg.ev.deco"],block_state:{Name:"minecraft:magma_block"},brightness:{sky:15,block:15},transformation:{translation:[-0.3f,0f,-0.3f],left_rotation:[0.2f,0.1f,0f,0.97f],scale:[0.6f,0.6f,0.6f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:husk ~2 ~ ~0 {Tags:["rpg.ev.star","rpg.ev.new"],PersistenceRequired:1b}
summon minecraft:zombie ~-2 ~ ~1 {Tags:["rpg.ev.star","rpg.ev.new"],PersistenceRequired:1b}
summon minecraft:skeleton ~0 ~ ~-2 {Tags:["rpg.ev.star","rpg.ev.new"],PersistenceRequired:1b}
scoreboard players set #sef rpg_el 4
execute as @a[distance=..64] if score @s rpg_sef > #sef rpg_el run scoreboard players operation #sef rpg_el = @s rpg_sef
execute as @e[tag=rpg.ev.new] at @s run function rpg:elite/make
tag @e[tag=rpg.ev.new] remove rpg.ev.new
