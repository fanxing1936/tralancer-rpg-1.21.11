tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#C9A646","bold":true,"italic":false},{"text":"神父","color":"#C9A646","bold":true,"italic":false},{"text":"〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔉𝔞𝔱𝔥𝔢𝔯","color":"#8F7430","italic":false},{"text":"  它跪下了。由你来裁决：消灭、放逐，还是封印。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"It kneels. The verdict is yours: destroy, banish, or seal.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.pr17 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
scoreboard players set #ph rpg_te 4
execute as @e[tag=rpg.te.fly] run function rpg:town/ev/remove
execute as @e[type=minecraft:vindicator,tag=rpg.te.av] run data merge entity @s {NoAI:1b,Invulnerable:1b}
execute as @a[tag=rpg.tw.in] run function rpg:town/ev/g/verdict
