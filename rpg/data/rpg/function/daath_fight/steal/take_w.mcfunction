scoreboard players set @s rpg_dt_sw 800
scoreboard players set @s rpg_dt_sp 0
execute store result score #s rpg_dt run data get entity @a[tag=rpg.dt.me,limit=1] SelectedItemSlot
execute store result storage rpg:daath t.hs int 1 run scoreboard players get #s rpg_dt
execute as @a[tag=rpg.dt.me,limit=1] at @s run function rpg:daath_fight/snap/all_one
function rpg:daath_fight/steal/store_w with storage rpg:daath t
item replace entity @a[tag=rpg.dt.me,limit=1] weapon.mainhand with minecraft:air
scoreboard players set @a[tag=rpg.dt.me,limit=1] rpg_dt_got 1
function rpg:daath_fight/weapon/stolen
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"text":"影","color":"#AAB4C3","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"这是我的了。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　This is mine now.","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s22 voice @s ~ ~ ~ 1 1 1
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"它夺走了你的武器：伤害 +20%。灯下打中它四下，或让它眩晕，就能拿回来。","color":"#FF5A62","bold":false,"italic":false}]
playsound rpg:daath.execute hostile @a[distance=..48] ~ ~ ~ 1.2 0.9
playsound minecraft:entity.item.break hostile @a[distance=..48] ~ ~ ~ 1 0.6
