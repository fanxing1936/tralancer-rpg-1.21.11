tag @s add rpg.xm.4
loot give @s loot rpg:forge/rune_any
loot give @s loot rpg:forge/stone_any
loot give @s loot rpg:world/bp_epic_any
tellraw @s ["",{"text":"〖见闻录〗","color":"#C9A646","bold":true,"italic":false},{"text":"  探索点到了 800：符文、符石、史诗图纸","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.6 1.1
