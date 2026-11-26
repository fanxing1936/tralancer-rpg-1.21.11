# positioned 场地中心，as 玩家
function rpg:daath_fight/slot/sweep
function rpg:daath_fight/arena/build
function rpg:daath_fight/arena/props
scoreboard players operation @e[type=minecraft:marker,tag=rpg.dt.c,distance=..4] rpg_dt = @s rpg_dt
scoreboard players operation @e[type=minecraft:marker,tag=rpg.dt.c,distance=..4] rpg_dt_sid = @s rpg_dt_sid
