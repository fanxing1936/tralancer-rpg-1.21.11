# 失败：一半奖励，镇子第二天自己修好
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#FF6B5E","bold":true,"italic":false},{"text":"  这一夜没守住……失败也有一半的收获。","color":"#9C9A94","bold":false,"italic":false}]
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#C9B27A","bold":true,"italic":false},{"text":"村长","color":"#C9B27A","bold":true,"italic":false},{"text":"〗","color":"#C9B27A","bold":true,"italic":false},{"text":" 𝔈𝔩𝔡𝔢𝔯","color":"#8F7430","italic":false},{"text":"  昨晚的事别往心里去。镇子挨过比这更糟的夜。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Don't take last night to heart. This town has survived worse nights.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.el07 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
execute as @a[tag=rpg.tw.in] run function rpg:town/ev/reward_half
function rpg:town/ev/stop
