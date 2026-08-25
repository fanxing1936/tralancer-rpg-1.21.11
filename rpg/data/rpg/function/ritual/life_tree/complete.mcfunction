tag @s add rpg.lt.complete
execute as @a[tag=rpg.kabbalah.user,distance=..5,sort=nearest,limit=1] unless score @s rpg_lt_claim matches 1.. run function rpg:ritual/life_tree/give_old_covenant
scoreboard players set @a[tag=rpg.kabbalah.user,distance=..5,sort=nearest,limit=1] rpg_lt_claim 1
particle minecraft:flash{color:13145394} ~ ~0.18 ~ 0 0 0 0 1 force
particle minecraft:totem_of_undying ~ ~0.35 ~ 2.2 0.35 4.6 0.10 140 force
playsound minecraft:ui.toast.challenge_complete master @a[distance=..32] ~ ~ ~ 1.0 0.82
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[旧约] ","color":"#D4AF37","bold":true,"italic":false},{"text":"十源质归位，律法的上半部显于人间；","color":"gray","bold":false,"italic":false},{"text":"Daath 节点","color":"#62D9E8","bold":true,"italic":false},{"text":"仍等待最后的见证。","color":"gray","bold":false,"italic":false}]
