scoreboard players set #ct rpg_pr 0
kill @e[type=minecraft:item_display,tag=rpg.pr.cam]
execute in rpg:armageddon run summon minecraft:item_display 0 120 0 {Tags:["rpg.pr.cam","rpg.pr.ent"],teleport_duration:0}
gamemode spectator @a[tag=rpg.pr]
execute as @a[tag=rpg.pr] run spectate @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] @s
