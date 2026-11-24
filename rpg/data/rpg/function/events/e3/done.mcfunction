execute as @a[distance=..48,gamemode=!spectator] run function rpg:events/e3/reward
tellraw @a ["",{"text":"〖事件・罪仆巡逻〗","color":"#A276BE","bold":true,"italic":false},{"text":" 𝔊𝔬𝔢𝔱𝔦𝔠 𝔓𝔞𝔱𝔯𝔬𝔩","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"巡逻的罪仆都倒下了。","color":"#9C9A94","bold":false,"italic":false}]
function rpg:events/end
