Для того чтобы добавить компонентв в HA, нужно в файле configuration.yaml добавить:
```yaml
light:
  - platform: simple_light
    host: simple_light
    port: 4444
```