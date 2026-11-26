# as/at 影子；挑战者带 rpg.dt.me
tag @s remove rpg.dt.new
scoreboard players operation @s rpg_dt = @a[tag=rpg.dt.me,limit=1] rpg_dt
scoreboard players operation @s rpg_dt_sid = @a[tag=rpg.dt.me,limit=1] rpg_dt_sid
scoreboard players set @s rpg_dt_st 1
scoreboard players set @s rpg_dt_sk 0
scoreboard players set @s rpg_dt_t 0
scoreboard players set @s rpg_dt_cl 0
scoreboard players set @s rpg_dt_far 0
scoreboard players set @s rpg_dt_still 0
scoreboard players set @s rpg_dt_mel 0
scoreboard players set @s rpg_dt_melt 0
scoreboard players set @s rpg_dt_same 0
scoreboard players set @s rpg_dt_ek 0
scoreboard players set @s rpg_dt_et 0
scoreboard players set @s rpg_dt_eid 0
scoreboard players set @s rpg_dt_esm 0
scoreboard players set @s rpg_dt_ult 0
scoreboard players set @s rpg_dt_lit 0
scoreboard players set @s rpg_dt_blade 0
scoreboard players set @s rpg_dt_sw 0
scoreboard players set @s rpg_dt_sa 0
scoreboard players set @s rpg_dt_shell 0
scoreboard players set @s rpg_dt_tries 0
scoreboard players set @s rpg_dt_die 0
scoreboard players set @s rpg_dt_dsp 0
scoreboard players set @s rpg_dt_orb 0
scoreboard players set @s rpg_dt_bgm 0
scoreboard players set @s rpg_dt_say 0
scoreboard players set @s rpg_dt_scd 400
scoreboard players set @s rpg_dt_gcd 120
scoreboard players set @s rpg_dt_gap 30
scoreboard players set @s rpg_dt_slot -1
# 每段生命 = 挑战者的近战面板 ×60，900 到 3000；手里不是武器就 1200（虚拟血池，不受原版 1024 上限管）
scoreboard players set @s rpg_dt_mx 1200
execute if items entity @a[tag=rpg.dt.me,limit=1] weapon.mainhand #rpg:daath/weapon store result score @s rpg_dt_mx run attribute @a[tag=rpg.dt.me,limit=1] minecraft:attack_damage get 60
execute if score @s rpg_dt_mx matches ..899 run scoreboard players set @s rpg_dt_mx 900
execute if score @s rpg_dt_mx matches 3001.. run scoreboard players set @s rpg_dt_mx 3000
function rpg:daath_fight/unit/refill
function rpg:daath/dress
function rpg:daath/wear/all
function rpg:daath/look/dark
function rpg:daath_fight/weapon/pick
scoreboard players set @s rpg_dt_sk 27
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
function rpg:daath/anim/enter/revive
function rpg:daath_fight/bar/open
function rpg:daath_fight/music/1
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"text":"影","color":"#AAB4C3","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"你下来得比我想的晚。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　You came down later than I thought you would.","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s01 voice @s ~ ~ ~ 1 1 1
execute if score @a[tag=rpg.dt.me,limit=1] rpg_dt_n matches 1.. run function rpg:daath_fight/say_n02
