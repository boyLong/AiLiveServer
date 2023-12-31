-- upgrade --
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` BIGINT NOT NULL  COMMENT '用户手机号',
    `password` VARCHAR(255) NOT NULL  COMMENT '用户密码',
    `is_allow` BOOL NOT NULL  COMMENT '是否能用' DEFAULT 0,
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `Expire_at` DATETIME(6) NOT NULL  COMMENT '到期时间' DEFAULT CURRENT_TIMESTAMP(6),
    KEY `idx_user_usernam_9987ab` (`username`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `Ex_Code` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `code` VARCHAR(255) NOT NULL  COMMENT '激活码',
    `used` BOOL NOT NULL  COMMENT '是否使用过' DEFAULT 0,
    `ex_time` INT NOT NULL  COMMENT '可用天数' DEFAULT 0,
    `remark` VARCHAR(255) NOT NULL  COMMENT '备注',
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_Ex_Code_user_c58f14a1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    KEY `idx_Ex_Code_code_4043b7` (`code`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `group` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `groupName` VARCHAR(255) NOT NULL,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_group_user_ad5cc84a` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `Reply_Tag` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `tag_name` VARCHAR(255) NOT NULL,
    `keywords` JSON NOT NULL  COMMENT '匹配关键词',
    `voice_link` LONGTEXT NOT NULL  COMMENT '视频链接',
    `group_id_id` INT NOT NULL,
    CONSTRAINT `fk_Reply_Ta_group_ce73ce49` FOREIGN KEY (`group_id_id`) REFERENCES `group` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `voice` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `VideosLink` VARCHAR(255) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
