scoreboard players set @s rpg_ex_kind 7
scoreboard players set @s rpg_ex_ransom 1
scoreboard players set @s rpg_ex_ctime 200
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[反仪式·贪婪] ","color":"#FFD85A","bold":true,"italic":false},{"text":"玛门暂停宣判，要求赎金： ","color":"gray","italic":false},{"text":"[支付3级]","color":"aqua","bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_ex_choice set 11"},"italic":false},{"text":"  ","color":"white","italic":false},{"text":"[献出4心]","color":"red","bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_ex_choice set 12"},"italic":false},{"text":"  ","color":"white","italic":false},{"text":"[交出金锭]","color":"gold","bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_ex_choice set 13"},"italic":false}]
playsound minecraft:block.vault.activate hostile @a[distance=..20] ~ ~ ~ 1 0.65
