tag @s add rpg.tl.bp
tellraw @s ["",{"text":"〖","color":"#C9B27A","bold":true,"italic":false},{"text":"村长","color":"#C9B27A","bold":true,"italic":false},{"text":"〗","color":"#C9B27A","bold":true,"italic":false},{"text":" 𝔈𝔩𝔡𝔢𝔯","color":"#8F7430","italic":false},{"text":"  这张图纸是镇上的老手艺，只给自己人。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"This pattern is the town's old craft. We only give it to our own.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.el05 voice @s ~ ~ ~ 1 1
loot give @s loot rpg:world/bp_epic_any
