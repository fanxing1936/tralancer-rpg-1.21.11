execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.lucifer,distance=0..] run function rpg:prologue_lucifer/anim/enter/pit_rise
function rpg:prologue_i1/sub/x01
execute as @a[tag=rpg.pri1] at @s run playsound minecraft:entity.warden.heartbeat master @s ~ ~ ~ 1.2 0.6
