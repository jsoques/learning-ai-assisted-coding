var builder = DistributedApplication.CreateBuilder(args);

var mailpit = builder.AddContainer("mailpit", "axllent/mailpit")
    .WithHttpEndpoint(targetPort: 8025, name: "http")
    .WithEndpoint(targetPort: 1025, name: "smtp");

var projectRoot = Path.GetFullPath(Path.Combine(Directory.GetCurrentDirectory(), "..", ".."));
var wrapperPath = Path.Combine(projectRoot, "src", "framework", "otel_wrapper.sh");
var pythonPath = Path.Combine(projectRoot, ".venv", "bin", "python");

var api = builder.AddExecutable("ecommerce-api", wrapperPath, projectRoot,
        pythonPath, "-m", "src.framework.main")
    .WithHttpEndpoint(targetPort: 5566, name: "http")
    .WithEnvironment("DATABASE_URL", "sqlite:///data/ecommerce.db")
    .WithEnvironment("MAILPIT_URL", mailpit.GetEndpoint("http"))
    .WithEnvironment("JWT_SECRET", "dev-secret-change-in-production")
    .WithEnvironment("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:19090")
    .WaitFor(mailpit);

builder.Build().Run();
