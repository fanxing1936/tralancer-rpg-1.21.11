scoreboard players set #f rpg_dt 1
scoreboard players set @s rpg_dt_sa 800
scoreboard players set @s rpg_dt_sp 0
execute at @s run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.dt.ret"]}
item replace entity @e[type=minecraft:item_display,tag=rpg.dt.ret,limit=1] contents from entity @a[tag=rpg.dt.me,limit=1] armor.legs
data modify storage rpg:daath t.e set value {slot:"armor.legs"}
data modify storage rpg:daath t.e.item set from entity @e[type=minecraft:item_display,tag=rpg.dt.ret,limit=1] item
kill @e[type=minecraft:item_display,tag=rpg.dt.ret]
function rpg:daath_fight/steal/store_a with storage rpg:daath t
item replace entity @a[tag=rpg.dt.me,limit=1] armor.legs with minecraft:air
scoreboard players set @a[tag=rpg.dt.me,limit=1] rpg_dt_got 1
execute on passengers if entity @s[tag=rpg.dtm.s.legs] run data merge entity @s {brightness:{block:15,sky:15}}
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"text":"影","color":"#AAB4C3","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"这是我的了。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　This is mine now.","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s22 voice @s ~ ~ ~ 1 1 1
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"它夺走了你的盔甲：受到的伤害 −20%。灯下打中它四下，或让它眩晕，就能拿回来。","color":"#FF5A62","bold":false,"italic":false}]
playsound rpg:daath.execute hostile @a[distance=..48] ~ ~ ~ 1.2 0.8
playsound minecraft:item.armor.equip_netherite hostile @a[distance=..48] ~ ~ ~ 1 0.6
