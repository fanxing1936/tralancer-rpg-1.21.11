tag @s add rpg.tl.guardian
tellraw @s ["",{"text":"〖","color":"#C9B27A","bold":true,"italic":false},{"text":"村长","color":"#C9B27A","bold":true,"italic":false},{"text":"〗","color":"#C9B27A","bold":true,"italic":false},{"text":" 𝔈𝔩𝔡𝔢𝔯","color":"#8F7430","italic":false},{"text":"  从今天起，你就是这个镇的守护者。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"From today on, you are this town's guardian.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.el06 voice @s ~ ~ ~ 1 1
function rpg:quest/title/get_guardian
