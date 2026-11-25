# 每秒：先定该放什么（w），再和正在放的（c）比
execute if score @s rpg_bgm_lv matches 1.. run function rpg:bgm/rejoin
scoreboard players add @s rpg_bgm_c 0
scoreboard players add @s rpg_bgm_t 0
scoreboard players set @s rpg_bgm_w 0
execute if dimension minecraft:overworld run function rpg:bgm/want_ow
execute if dimension rpg:paradise_lost run function rpg:bgm/want_pl
execute unless score @s rpg_bgm_w matches 0 run function rpg:bgm/yield
execute if score @s rpg_bgm_w matches 0 if score @s rpg_bgm_c matches 0 run return 0
execute if score @s rpg_bgm_w matches 0 run return run function rpg:bgm/stop
stopsound @s music
execute if score @s rpg_bgm_c = @s rpg_bgm_w run return run function rpg:bgm/same
execute if score @s rpg_bgm_c matches 0 run return run function rpg:bgm/begin
# 昼夜交替：不打断，只换后面的曲单
execute if score @s rpg_bgm_c matches 10..11 if score @s rpg_bgm_w matches 10..11 run return run function rpg:bgm/shift
# 换区：稳 3 秒才换（还在放的曲子照常计时）
scoreboard players add @s rpg_bgm_s 1
scoreboard players remove @s rpg_bgm_t 1
execute if score @s rpg_bgm_s matches 3.. run function rpg:bgm/swap
