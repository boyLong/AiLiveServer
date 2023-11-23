-- upgrade --
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` INT NOT NULL  COMMENT '用户手机号',
    `password` VARCHAR(255) NOT NULL  COMMENT '用户密码',
    `is_allow` BOOL NOT NULL  COMMENT '是否能用' DEFAULT 0,
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `Expire_at` DATETIME(6) NOT NULL  COMMENT '到期时间' DEFAULT CURRENT_TIMESTAMP(6),
    KEY `idx_user_usernam_9987ab` (`username`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
