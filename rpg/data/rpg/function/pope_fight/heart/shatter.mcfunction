execute positioned ~ ~3 ~ run function rpg:pope_fight/fx/burst_void
particle dust{color:[0.835f,0.588f,0.949f],scale:1.6} ~ ~3 ~ 1.5 2 1.5 0.2 96 force
particle flash{color:13997810} ~ ~3 ~ 0 0 0 0 1 force
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] at @s run function rpg:heart_of_ender/internal/clear
