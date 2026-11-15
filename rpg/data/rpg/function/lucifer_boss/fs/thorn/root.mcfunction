summon minecraft:marker ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lub.thorn"]}
execute as @e[type=minecraft:marker,tag=rpg.lu2f.pnew,tag=rpg.lub.thorn] run tp @s ^ ^ ^2 ~ ~
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 11
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 40
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
