# 收回契约：七罪契约进入 15 秒冷却。
scoreboard players set @e[tag=rpg.unit.f,distance=..40] rpg_pact_cd 300
scoreboard players set @e[tag=rpg.unit.f,distance=..40,scores={rpg_pact_cd2=..300}] rpg_pact_cd2 300
scoreboard players set @e[tag=rpg.unit.f,distance=..40,scores={rpg_pact_cd3=..300}] rpg_pact_cd3 300
execute as @e[tag=rpg.unit.f,distance=..40] at @s run particle enchant ~ ~1 ~ 0.5 1 0.5 0.5 24 normal
execute as @e[tag=rpg.unit.f,distance=..40] at @s run function rpg:pope_fight/fx/chain
tellraw @a[tag=!rpg.fo.msh,distance=..48] ["",{"text":"〖教皇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"你借来的力量，账本在我手里。","color":"#9C9A94","bold":false,"italic":false}]
playsound rpg:pope.laugh hostile @a[tag=!rpg.fo.msh,distance=..32] ~ ~ ~ 1 1
