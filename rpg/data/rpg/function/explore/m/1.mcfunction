tag @s add rpg.xm.1
loot give @s loot rpg:forge/rune_any
loot give @s loot rpg:forge/item/forge_stone
tellraw @s ["",{"text":"〖见闻录〗","color":"#C9A646","bold":true,"italic":false},{"text":"  探索点到了 150：符文 ×1、锻石 ×1","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.6 1.1
