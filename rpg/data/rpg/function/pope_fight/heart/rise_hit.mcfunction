# 破土：离得太近的玩家被掀飞。
execute as @a[distance=..4,gamemode=!spectator,gamemode=!creative] run damage @s 14 minecraft:indirect_magic by @e[type=minecraft:vindicator,tag=rpg.pf.heart,limit=1]
function rpg:pope_fight/fx/shock_big
particle dust{color:[0.835f,0.588f,0.949f],scale:1.6} ~ ~0.5 ~ 2 0.3 2 0.1 24 normal
