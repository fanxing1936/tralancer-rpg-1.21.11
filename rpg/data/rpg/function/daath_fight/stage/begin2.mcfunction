tag @s remove rpg.dt.morph
tag @s remove rpg.dt.u1
tag @s remove rpg.dt.u2
tag @s remove rpg.dt.u3
scoreboard players set @s rpg_dt_st 2
scoreboard players set @s rpg_dt_bar -1
function rpg:daath_fight/unit/refill
function rpg:daath_fight/bar/set
function rpg:daath_fight/music/2
scoreboard players set @s rpg_dt_gap 20
scoreboard players set @s rpg_dt_scd 200
attribute @s minecraft:movement_speed base set 0.39
function rpg:daath_fight/sk/end
function rpg:daath_fight/say_deaths
title @a[tag=rpg.dt.me,limit=1] times 5 35 12
title @a[tag=rpg.dt.me,limit=1] subtitle ["",{"text":"𝔉𝔞𝔠𝔦𝔢 𝔞𝔡 𝔉𝔞𝔠𝔦𝔢𝔪","color":"#8F7430","bold":false,"italic":false}]
title @a[tag=rpg.dt.me,limit=1] title ["",{"text":"面对面","color":"#FFFFFF","bold":true,"italic":false}]
