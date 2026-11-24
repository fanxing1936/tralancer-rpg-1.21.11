function rpg:events/place_near
function rpg:events/e1/begin
scoreboard players set #tide rpg_ev 1
scoreboard players set @a rpg_ev_tc 0
tag @a remove rpg.ev.yesod
tellraw @a ["",{"text":"〖事件・罪潮之夜〗","color":"#C77298","bold":true,"italic":false},{"text":" 𝔗𝔦𝔡𝔢 𝔬𝔣 𝔖𝔦𝔫","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"今夜罪孽涨潮。精英成群出没，残魂也比往常更多（10 分钟）。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:ambient.cave master @a ~ ~ ~ 1 0.5
