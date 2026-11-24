# 扣料、给罪器（与驱魔「契约」结局给的是同一件）
clear @s minecraft:nether_star[minecraft:custom_data~{rpg_weapon_core:1b,rpg_lord:4}] 1
execute store result storage rpg:forge d.k int 1 run scoreboard players get #need_s rpg_fg
function rpg:forge/sin/take_shard_4 with storage rpg:forge d
execute if score #need_n rpg_fg matches 1 run clear @s minecraft:netherite_ingot[!minecraft:custom_data] 1
clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 8
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
scoreboard players add @s rpg_taint 15
function rpg:inquest/give/pact_weapon4
execute at @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8,limit=1,sort=nearest] run particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.3 0.5 0.3 0.05 60
execute at @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8,limit=1,sort=nearest] run particle minecraft:dust{color:[0.71,0.85,0.34],scale:1.4} ~ ~1 ~ 0.4 0.6 0.4 0 40
playsound minecraft:block.end_portal.spawn player @s ~ ~ ~ 0.6 0.8
playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 1 0.6
tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　罪器在魂火里凝结：","color":"#9C9A94","bold":false,"italic":false},{"text":"[恶魔]","color":"#B5D957","bold":true,"italic":false},{"text":"别西卜","color":"#E6DFCF","bold":true,"italic":false},{"text":"　魔化 +15","color":"#C04A3C","bold":false,"italic":false}]
