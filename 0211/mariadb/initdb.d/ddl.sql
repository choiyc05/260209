USE edu;

CREATE TABLE edu.`file` (
    `no`                 INT                 NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `origin`         VARCHAR(100)    NOT NULL,
    `ext`                VARCHAR(10)        NOT NULL, 
    `fileName`        VARCHAR(100)    NOT NULL,
    `contentType`    VARCHAR(20)        NOT NULL,
    `regDate`         DATETIME       NOT NULL COMMENT '회원등록일자'        DEFAULT CURRENT_TIMESTAMP,
   `modDate`         DATETIME       NOT NULL COMMENT '회원정보수정일자' DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

COMMIT;