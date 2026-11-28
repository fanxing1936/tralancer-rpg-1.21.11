scoreboard players set #ct rpg_pr_i2 0
kill @e[type=minecraft:item_display,tag=rpg.pr.cam,distance=0..]
execute in rpg:armageddon_2 run summon minecraft:item_display 0 120 0 {Tags:["rpg.pr.cam","rpg.pr.ent"],teleport_duration:0}
gamemode spectator @a[tag=rpg.pri2]
execute as @a[tag=rpg.pri2] run spectate @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] @s
