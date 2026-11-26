execute if score @s rpg_dt_t matches 1..58 run execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute if score @s rpg_dt_t matches 10..60 at @s run particle minecraft:end_rod ^ ^1.2 ^3.5 0.05 0.05 1.6 0 2
execute if score @s rpg_dt_t matches 10 run function rpg:daath_fight/clash/pulse
execute if score @s rpg_dt_t matches 22 run function rpg:daath_fight/clash/pulse
execute if score @s rpg_dt_t matches 34 run function rpg:daath_fight/clash/pulse
execute if score @s rpg_dt_t matches 44 run function rpg:daath_fight/clash/pulse
execute if score @s rpg_dt_t matches 52 run function rpg:daath_fight/clash/pulse
execute if score @s rpg_dt_t matches 52 run execute at @a[tag=rpg.dt.me,limit=1] run summon minecraft:interaction ~ ~-0.5 ~ {Tags:["rpg.dt.clk"],width:4f,height:4f,response:0b}
execute if score @s rpg_dt_t matches 53..66 run execute if entity @s[tag=rpg.dt.window] run function rpg:daath_fight/clash/listen
execute if score @s rpg_dt_t matches 67 run kill @e[type=minecraft:interaction,tag=rpg.dt.clk,distance=..60]
execute if score @s rpg_dt_t matches 52 run tag @s add rpg.dt.window
execute if score @s rpg_dt_t matches 52 run playsound minecraft:block.bell.use hostile @a[distance=..48] ~ ~ ~ 1 1.6
execute if score @s rpg_dt_t matches 60 run function rpg:daath/anim/enter/cl3
execute if score @s rpg_dt_t matches 66 run function rpg:daath_fight/clash/fall
execute if score @s rpg_dt_t matches 96.. run function rpg:daath_fight/sk/end
