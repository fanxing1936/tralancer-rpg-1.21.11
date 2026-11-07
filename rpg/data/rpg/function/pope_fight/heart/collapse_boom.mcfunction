# 外壳也炸开了：之后这几秒是破绽。
execute as @a[distance=..15,gamemode=!spectator,gamemode=!creative] run damage @s 30 minecraft:indirect_magic by @e[type=minecraft:vindicator,tag=rpg.pf.heart,limit=1]
execute positioned ~ ~3 ~ run function rpg:pope_fight/fx/flare_burst
particle dust{color:[0.835f,0.588f,0.949f],scale:1.6} ~ ~1 ~ 6 1 6 0.3 80 normal
particle flash{color:13997810} ~ ~3 ~ 0 0 0 0 1 normal
playsound rpg:heart_of_ender.mortar_explode hostile @a[distance=..64] ~ ~ ~ 1.5 0.5
playsound minecraft:entity.generic.explode hostile @a[distance=..64] ~ ~ ~ 1.5 0.6
function rpg:pope_fight/heart/weak_on
function rpg:pope_fight/heart/clip/idle
