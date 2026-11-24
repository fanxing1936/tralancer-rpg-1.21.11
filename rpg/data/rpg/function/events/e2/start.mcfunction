function rpg:events/place
function rpg:events/e2/begin
scoreboard players set #stage rpg_ev 0
tellraw @a ["",{"text":"〖事件・坠星〗","color":"#FFF2A8","bold":true,"italic":false},{"text":" 𝔉𝔞𝔩𝔩𝔦𝔫𝔤 𝔖𝔱𝔞𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"一颗星从天上落下来了。","color":"#9C9A94","bold":false,"italic":false},{"text":"　坐标 ","color":"#9C9A94","bold":false,"italic":false},{"nbt":"cur.x","storage":"rpg:events","color":"#E6DFCF"},{"text":", ","color":"#9C9A94","bold":false,"italic":false},{"nbt":"cur.z","storage":"rpg:events","color":"#E6DFCF"}]
playsound minecraft:entity.firework_rocket.launch master @a ~ ~ ~ 1 0.5
