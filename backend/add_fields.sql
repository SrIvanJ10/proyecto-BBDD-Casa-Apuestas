-- Añadir campos al modelo Partido
ALTER TABLE sportpredict_partido 
ADD COLUMN IF NOT EXISTS goles_local INTEGER NULL,
ADD COLUMN IF NOT EXISTS goles_visitante INTEGER NULL,
ADD COLUMN IF NOT EXISTS amarillas_local INTEGER NULL,
ADD COLUMN IF NOT EXISTS amarillas_visitante INTEGER NULL,
ADD COLUMN IF NOT EXISTS rojas_local INTEGER NULL,
ADD COLUMN IF NOT EXISTS rojas_visitante INTEGER NULL,
ADD COLUMN IF NOT EXISTS expulsiones_local INTEGER NULL,
ADD COLUMN IF NOT EXISTS expulsiones_visitante INTEGER NULL,
ADD COLUMN IF NOT EXISTS mvp_jugador VARCHAR(100) NULL;

-- Añadir campos al modelo Prediccion
ALTER TABLE sportpredict_prediccion
ADD COLUMN IF NOT EXISTS pred_goles_local INTEGER NULL,
ADD COLUMN IF NOT EXISTS pred_goles_visitante INTEGER NULL,
ADD COLUMN IF NOT EXISTS pred_amarillas_local INTEGER NULL,
ADD COLUMN IF NOT EXISTS pred_amarillas_visitante INTEGER NULL,
ADD COLUMN IF NOT EXISTS pred_rojas_local INTEGER NULL,
ADD COLUMN IF NOT EXISTS pred_rojas_visitante INTEGER NULL,
ADD COLUMN IF NOT EXISTS pred_expulsiones_local INTEGER NULL,
ADD COLUMN IF NOT EXISTS pred_expulsiones_visitante INTEGER NULL,
ADD COLUMN IF NOT EXISTS pred_mvp_jugador VARCHAR(100) NULL,
ADD COLUMN IF NOT EXISTS puntos_resultado INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS puntos_tarjetas INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS puntos_mvp INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS puntos_totales INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS evaluada BOOLEAN DEFAULT FALSE;

-- Hacer que el campo prediccion sea opcional (允许为空)
ALTER TABLE sportpredict_prediccion 
ALTER COLUMN prediccion DROP NOT NULL;
