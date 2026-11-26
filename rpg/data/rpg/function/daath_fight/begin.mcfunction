# 占一块场地、记下来处、拍快照（as/at 玩家，#slot 场地号）
scoreboard players operation @s rpg_dt = #slot rpg_dt
scoreboard players add #sid rpg_dt 1
scoreboard players operation @s rpg_dt_sid = #sid rpg_dt
scoreboard players set @s rpg_dt_ph 1
scoreboard players set @s rpg_dt_pt 0
scoreboard players set @s rpg_dt_dc 0
scoreboard players add @s rpg_dt_n 0
scoreboard players set @s rpg_dt_cast 0
scoreboard players set @s rpg_dt_drk 0
execute store result storage rpg:daath t.id int 1 run scoreboard players get @s rpg_fg_id
execute store result storage rpg:daath t.n int 1 run scoreboard players get @s rpg_dt
function rpg:daath_fight/begin_m with storage rpg:daath t
function rpg:daath_fight/snap/all
effect give @s minecraft:darkness 6 0 true
effect give @s minecraft:slowness 4 3 true
playsound minecraft:ambient.underwater.enter player @s ~ ~ ~ 1 0.5
playsound minecraft:block.conduit.deactivate player @s ~ ~ ~ 1 0.5
