# 离开深渊（任何原因）：先还东西，再送回来处，收场（as 玩家）
function rpg:daath_fight/steal/give_all
execute store result storage rpg:daath t.id int 1 run scoreboard players get @s rpg_fg_id
execute store result storage rpg:daath t.n int 1 run scoreboard players get @s rpg_dt
execute unless entity @s[tag=rpg.dt.dead] run function rpg:daath_fight/pl/back_m with storage rpg:daath t
function rpg:daath_fight/pl/close_m with storage rpg:daath t
tag @s remove rpg.dt.in
tag @s remove rpg.dt.me
tag @s remove rpg.dt.walk
tag @s remove rpg.dt.dead
scoreboard players set @s rpg_dt 0
scoreboard players set @s rpg_dt_ph 0
effect clear @s minecraft:levitation
effect clear @s minecraft:blindness
effect clear @s minecraft:darkness
effect give @s minecraft:slow_falling 3 0 true
stopsound @s record
playsound minecraft:ambient.underwater.exit player @s ~ ~ ~ 1 0.7
